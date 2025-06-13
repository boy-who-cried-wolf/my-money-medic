"""
Adaptive Quiz API endpoints for dynamic, personalized quiz experiences.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
import json
import logging
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import uuid

from app.database import get_db
from app.core.auth import get_current_user
from app.database.models.user import User, UserType
from app.database.models.quiz import UserQuizResponse, QuizQuestion, QuizCategory, Quiz
from app.services.adaptive_quiz_service import AdaptiveQuizService

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()


class TestFlowRequest(BaseModel):
    """Request model for test flow endpoint"""

    test_responses: List[Dict[str, Any]]


@router.post("/start", response_model=Dict[str, Any])
async def start_adaptive_quiz(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Start a new adaptive quiz session for the current user.
    If an incomplete session exists, it will be restored.

    Returns:
        Dict containing session info and first question
    """
    try:
        if current_user.user_type != UserType.CLIENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only clients can take adaptive quizzes",
            )

        # Check for existing incomplete quiz session
        existing_responses = (
            db.query(UserQuizResponse)
            .filter(UserQuizResponse.user_id == current_user.id)
            .order_by(UserQuizResponse.created_at.desc())
            .all()
        )

        logger.info(f"Found {len(existing_responses)} existing responses for user {current_user.id}")

        if existing_responses:
            # Get the most recent session ID from responses
            latest_response = existing_responses[0]
            logger.info(f"Latest response type: {type(latest_response.response)}")
            logger.info(f"Latest response data: {latest_response.response}")
            
            # Handle response data based on its type
            response_data = latest_response.response
            if isinstance(response_data, str):
                try:
                    response_data = json.loads(response_data)
                    logger.info(f"Successfully parsed response data from string")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse response data as JSON: {e}")
                    response_data = {"answer": response_data}
            
            if not isinstance(response_data, dict):
                logger.error(f"Response data is not a dictionary: {type(response_data)}")
                response_data = {"answer": str(response_data)}
            
            session_id = response_data.get("session_id")
            logger.info(f"Extracted session_id: {session_id}")
            
            if session_id:
                # Get all responses for this session
                session_responses = []
                for resp in existing_responses:
                    resp_data = resp.response
                    if isinstance(resp_data, str):
                        try:
                            resp_data = json.loads(resp_data)
                        except json.JSONDecodeError:
                            resp_data = {"answer": resp_data}
                    
                    if isinstance(resp_data, dict) and resp_data.get("session_id") == session_id:
                        session_responses.append(resp)
                
                logger.info(f"Found {len(session_responses)} responses for session {session_id}")
                
                # Check if quiz was completed (should have 10 responses)
                if len(session_responses) >= 10:
                    logger.info(f"Found completed quiz session with {len(session_responses)} responses")
                    # Restore the completed session
                    adaptive_service = AdaptiveQuizService(db)
                    result = await adaptive_service.restore_quiz_session(
                        current_user.id, 
                        session_id,
                        session_responses
                    )
                    
                    # Add completion status and final insights
                    result["completed"] = True
                    result["reason"] = "quiz_completed"
                    
                    # Generate final insights and recommendations
                    try:
                        final_insights = await adaptive_service._generate_final_insights(result["session"])
                        recommendations = await adaptive_service._generate_recommendations(
                            result["session"], 
                            await adaptive_service._get_broker_matches(session_id)
                        )
                        result["insights"] = final_insights
                        result["recommendations"] = recommendations
                    except Exception as e:
                        logger.error(f"Error generating final insights: {str(e)}")
                    
                    return {
                        "success": True,
                        "data": result,
                        "message": "Completed quiz session restored",
                    }

        # If no incomplete session found, start a new one
        logger.info("Starting new quiz session")
        adaptive_service = AdaptiveQuizService(db)
        result = await adaptive_service.start_adaptive_quiz(current_user.id)

        # Create a new quiz record for this session
        session_id = result.get("session", {}).get("session_id")
        if session_id:
            # Create a new quiz for this session
            new_quiz = Quiz(
                title=f"Adaptive Quiz Session {session_id}",
                description=f"Adaptive quiz session for user {current_user.id}",
                category=QuizCategory.FINANCIAL_GOALS
            )
            db.add(new_quiz)
            db.commit()
            db.refresh(new_quiz)
            
            # Store quiz_id in session data
            result["session"]["quiz_id"] = new_quiz.id
            logger.info(f"Created new quiz with ID {new_quiz.id} for session {session_id}")

        return {
            "success": True,
            "data": result,
            "message": "Adaptive quiz session started successfully",
        }

    except ValueError as e:
        logger.error(f"ValueError in start_adaptive_quiz: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error starting adaptive quiz: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting adaptive quiz: {str(e)}",
        )


@router.post("/respond", response_model=Dict[str, Any])
async def submit_response_and_continue(
    session_data: Dict[str, Any],
    response: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Submit a response to the current question and get the next question.

    Args:
        session_data: Current quiz session data containing session info and question plan
        response: User's response to the current question

    Returns:
        Dict containing next question or completion results
    """
    try:
        logger.info(f"Received response data type: {type(response)}")
        logger.info(f"Received response data: {json.dumps(response)}")
        logger.info(f"Received session data type: {type(session_data)}")
        logger.info(f"Received session data: {json.dumps(session_data)}")

        # Verify user owns this session
        if session_data.get("user_id") != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only respond to your own quiz sessions",
            )

        # Format response data to ensure consistent structure
        answer = response.get("answer", "")
        if isinstance(answer, (int, float)):
            answer = str(answer)

        # Create the response object in the format expected by the service
        formatted_response = {
            "question_id": response.get("question_id"),
            "answer": answer,
            "response": response.get("response", {
                "answer": answer,
                "question_text": session_data.get("current_question_text"),
                "session_id": session_data.get("session_id"),
                "question_order": session_data.get("current_question"),
                "submitted_at": datetime.utcnow().isoformat()
            })
        }
        logger.info(f"Formatted response data type: {type(formatted_response)}")
        logger.info(f"Formatted response data: {json.dumps(formatted_response)}")

        # Create a new session data with only the current response
        current_question = session_data.get("current_question")
        current_response = {
            "question_number": current_question,
            "response": {
                "answer": formatted_response["response"]["answer"],
                "question_text": session_data.get("current_question_text"),
                "session_id": session_data.get("session_id"),
                "question_order": current_question,
                "submitted_at": datetime.utcnow().isoformat()
            },
            "question_text": session_data.get("current_question_text"),
            "timestamp": datetime.utcnow().isoformat()
        }

        # Update session data with only the current response
        session_data["responses"] = [current_response]

        adaptive_service = AdaptiveQuizService(db)
        logger.info("Calling submit_response_and_get_next with formatted data")
        result = await adaptive_service.submit_response_and_get_next(
            session_data, formatted_response
        )
        logger.info(f"Response processed successfully: {json.dumps(result)}")

        # Save response to database
        if "question_id" in response:
            question_id = response["question_id"]
            current_question = session_data.get("current_question", 1)
            question_plan = session_data.get("question_plan", [])
            
            logger.info(f"Question plan type: {type(question_plan)}")
            logger.info(f"Question plan: {json.dumps(question_plan)}")
            
            # Get current question details from plan
            current_question_details = next(
                (q for q in question_plan if q["order"] == current_question),
                None
            )
            
            logger.info(f"Current question details: {json.dumps(current_question_details) if current_question_details else 'None'}")
            logger.info(f"Attempting to save quiz response for user {current_user.id} to question {question_id}")
            logger.info(f"Response data: {json.dumps(formatted_response)}")

            # Check if question exists first
            existing_question = db.query(QuizQuestion).filter(QuizQuestion.id == question_id).first()
            
            if not existing_question:
                logger.info(f"Question {question_id} not found, creating new question record")
                
                # Get the quiz ID from session data or create a new quiz
                quiz_id = session_data.get("quiz_id")
                if not quiz_id:
                    # Create a new quiz for dynamic questions if needed
                    dynamic_quiz = db.query(Quiz).filter(Quiz.title == "Dynamic Questions").first()
                    if not dynamic_quiz:
                        dynamic_quiz = Quiz(
                            title="Dynamic Questions",
                            description="Questions generated dynamically during adaptive quizzes",
                            category=QuizCategory.FINANCIAL_GOALS
                        )
                        db.add(dynamic_quiz)
                        db.commit()
                        db.refresh(dynamic_quiz)
                    quiz_id = dynamic_quiz.id
                
                # Create a new question record with details from question plan
                new_question = QuizQuestion(
                    id=question_id,
                    quiz_id=quiz_id,
                    text=session_data.get("current_question_text", "Dynamic Question"),
                    question_type=current_question_details.get("type", "single_choice") if current_question_details else "single_choice",
                    options=[],  # Options are not stored for dynamic questions
                    order=current_question,
                    weight=1
                )
                db.add(new_question)
                db.commit()
                logger.info(f"Successfully created new question with ID {question_id}")
            
            # Now save the response
            db_response = UserQuizResponse(
                user_id=current_user.id,
                question_id=question_id,
                response=formatted_response["response"]
            )
            db.add(db_response)
            db.commit()
            db.refresh(db_response)
            
            logger.info(f"Successfully saved quiz response with ID {db_response.id}")
            logger.info(f"Saved response details: user_id={db_response.user_id}, question_id={db_response.question_id}")
        else:
            logger.warning(f"Could not save response - missing question_id in response data: {json.dumps(response)}")

        return {
            "success": True,
            "data": result,
            "message": "Response submitted successfully",
        }

    except ValueError as e:
        logger.error(f"Validation error while processing quiz response: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error saving quiz response: {str(e)}", exc_info=True)
        logger.error(f"Error occurred with response data: {json.dumps(response)}")
        logger.error(f"Error occurred with session data: {json.dumps(session_data)}")
        db.rollback()  # Rollback in case of error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing response: {str(e)}",
        )


@router.post("/generate-question", response_model=Dict[str, Any])
async def generate_dynamic_question(
    topic: str,
    category: str,
    question_type: str = "single_choice",
    context: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate a dynamic question for testing purposes.

    Args:
        topic: The topic for the question
        category: The category (FINANCIAL_GOALS, RISK_TOLERANCE, etc.)
        question_type: Type of question (single_choice, multiple_choice, scale, text)
        context: Optional context for question generation

    Returns:
        Generated question data
    """
    try:
        if current_user.user_type not in [UserType.ADMIN, UserType.BROKER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins and brokers can generate test questions",
            )

        adaptive_service = AdaptiveQuizService(db)

        # Create a mock session for question generation
        mock_session = {
            "user_id": current_user.id,
            "current_question": 1,
            "responses": context.get("previous_responses", []) if context else [],
            "focus_areas": context.get("focus_areas", []) if context else [],
            "insights": [],
        }

        question_data = await adaptive_service.quiz_generator.create_ai_question_data(
            topic=topic,
            category=category,
            question_type_str=question_type,
            order=1,
            existing_question_texts=[],
        )

        if not question_data:
            # Use fallback
            question_data = adaptive_service._get_fallback_question(topic, category, 1)

        # Save the generated question to database
        if "id" in question_data:
            # Create a new quiz for test questions if needed
            test_quiz = db.query(Quiz).filter(Quiz.title == "Test Questions").first()
            if not test_quiz:
                test_quiz = Quiz(
                    title="Test Questions",
                    description="Questions generated for testing purposes",
                    category=QuizCategory.FINANCIAL_GOALS
                )
                db.add(test_quiz)
                db.commit()
                db.refresh(test_quiz)

            # Create the question record
            new_question = QuizQuestion(
                id=question_data["id"],
                quiz_id=test_quiz.id,
                text=question_data.get("text", "Generated Question"),
                question_type=question_type,
                options=question_data.get("options", []),
                order=1,
                weight=1
            )
            db.add(new_question)
            db.commit()
            db.refresh(new_question)
            logger.info(f"Saved generated question with ID {new_question.id}")

        return {
            "success": True,
            "data": {
                "question": question_data,
                "generation_context": {
                    "topic": topic,
                    "category": category,
                    "question_type": question_type,
                    "generated_at": datetime.utcnow().isoformat(),
                },
            },
            "message": "Question generated successfully",
        }

    except Exception as e:
        logger.error(f"Error generating question: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating question: {str(e)}",
        )


@router.get("/session/{session_id}", response_model=Dict[str, Any])
async def get_quiz_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get quiz session data (for resuming or reviewing).

    Note: In a production system, you'd store session data in Redis or database.
    For now, this is a placeholder endpoint.
    """
    try:
        # In a real implementation, you'd retrieve session data from storage
        # For now, return a placeholder response
        return {
            "success": True,
            "data": {
                "session_id": session_id,
                "user_id": current_user.id,
                "status": "not_implemented",
                "message": "Session storage not implemented yet",
            },
            "message": "Session data retrieved (placeholder)",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving session: {str(e)}",
        )


@router.get("/insights/{user_id}", response_model=Dict[str, Any])
async def get_user_insights(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get AI-generated insights for a user based on their quiz responses.
    """
    try:
        # Compare against UserType enum values instead of strings
        if current_user.user_type == UserType.CLIENT and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own insights",
            )
        elif current_user.user_type == UserType.BROKER:
            # Brokers can only see insights for their matched clients
            # This would require checking if there's an active match
            pass
        elif current_user.user_type != UserType.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )

        # Get user's quiz responses
        from app.database.models.quiz import UserQuizResponse, QuizQuestion

        responses = (
            db.query(UserQuizResponse)
            .join(QuizQuestion)
            .filter(UserQuizResponse.user_id == user_id)
            .all()
        )

        if not responses:
            return {
                "success": True,
                "data": {
                    "insights": [],
                    "investment_profile": {
                        "investment_horizon": "Not assessed",
                        "risk_tolerance": "Not assessed",
                        "preferred_focus": "Not assessed",
                    },
                    "recommendations": [],
                    "broker_matches": [],
                    "message": "No quiz responses found for this user",
                },
            }

        # Simple direct approach - convert responses to working format
        response_data = []
        for i, resp in enumerate(responses[:10]):  # Limit to 10 for efficiency
            # Handle response format simply
            if isinstance(resp.response, str):
                try:
                    parsed_response = json.loads(resp.response)
                    answer = parsed_response.get("answer", str(parsed_response))
                except:
                    answer = resp.response
            else:
                answer = resp.response or "No response"

            response_data.append(
                {
                    "question_number": i + 1,
                    "question_text": resp.question.text,
                    "response": {"answer": answer},
                }
            )

        # Generate insights using the working direct approach
        adaptive_service = AdaptiveQuizService(db)

        # Generate investment profile (this works)
        try:
            investment_profile = adaptive_service._generate_investment_profile(
                response_data
            )
        except Exception as e:
            return {
                "success": False,
                "data": {"error": f"Investment profile error: {str(e)}"},
                "message": "Error generating investment profile",
            }

        # Generate insights (this works)
        session_data = {"user_id": user_id, "responses": response_data, "insights": []}

        try:
            insights = await adaptive_service._generate_final_insights(session_data)
        except Exception as e:
            return {
                "success": False,
                "data": {"error": f"Insights error: {str(e)}"},
                "message": "Error generating insights",
            }

        # Generate broker matches (this works)
        try:
            session_id = f"insights_{user_id}"
            adaptive_service._set_session(session_id, session_data)
            matches = await adaptive_service._get_broker_matches(session_id)
        except Exception as e:
            return {
                "success": False,
                "data": {"error": f"Matches error: {str(e)}"},
                "message": "Error generating matches",
            }

        # Generate recommendations (this works)
        try:
            recommendations = await adaptive_service._generate_recommendations(
                session_data, matches
            )
        except Exception as e:
            return {
                "success": False,
                "data": {"error": f"Recommendations error: {str(e)}"},
                "message": "Error generating recommendations",
            }

        return {
            "success": True,
            "data": {
                "user_id": user_id,
                "insights": insights,
                "recommendations": recommendations,
                "investment_profile": investment_profile,
                "broker_matches": matches,
                "quiz_session": {
                    "responses": response_data,
                    "total_responses": len(response_data),
                    "completion_status": "completed",
                },
                "total_responses": len(responses),
                "generated_at": "now",
            },
            "message": "Insights generated successfully",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating insights: {str(e)}",
        )


@router.post("/test-flow", response_model=Dict[str, Any])
async def test_adaptive_flow(
    request: TestFlowRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Test the adaptive quiz flow with predefined responses.
    Useful for testing and demonstration purposes.
    """
    try:
        # Compare against UserType enum instead of string
        if current_user.user_type != UserType.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can run test flows",
            )

        adaptive_service = AdaptiveQuizService(db)

        # Start quiz
        result = await adaptive_service.start_adaptive_quiz(current_user.id)
        session_data = result["session"]

        flow_results = []
        flow_results.append(
            {
                "step": "start",
                "question": result["question"],
                "progress": result["progress"],
            }
        )

        # Process test responses
        for i, test_response in enumerate(request.test_responses):
            try:
                result = await adaptive_service.submit_response_and_get_next(
                    session_data, test_response
                )

                flow_results.append(
                    {
                        "step": f"response_{i+1}",
                        "response_submitted": test_response,
                        "result": result,
                    }
                )

                # Update session data
                session_data = result.get("session", session_data)

                # Break if quiz is completed
                if result.get("completed"):
                    break

            except Exception as e:
                flow_results.append({"step": f"response_{i+1}_error", "error": str(e)})
                break

        return {
            "success": True,
            "data": {"test_flow_results": flow_results, "final_session": session_data},
            "message": "Test flow completed",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running test flow: {str(e)}",
        )


@router.post("/restart", response_model=Dict[str, Any])
async def restart_adaptive_quiz(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Restart the adaptive quiz for the current user.
    This will clear any existing responses and start fresh.
    """
    try:
        if current_user.user_type != UserType.CLIENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only clients can take adaptive quizzes",
            )

        # Delete all existing responses for this user
        db.query(UserQuizResponse).filter(UserQuizResponse.user_id == current_user.id).delete()
        db.commit()

        # Start a new quiz session
        adaptive_service = AdaptiveQuizService(db)
        result = await adaptive_service.start_adaptive_quiz(current_user.id)

        # Create a new quiz record for this session
        session_id = result.get("session", {}).get("session_id")
        if session_id:
            # Create a new quiz for this session
            new_quiz = Quiz(
                title=f"Adaptive Quiz Session {session_id}",
                description=f"Adaptive quiz session for user {current_user.id}",
                category=QuizCategory.FINANCIAL_GOALS
            )
            db.add(new_quiz)
            db.commit()
            db.refresh(new_quiz)
            
            # Store quiz_id in session data
            result["session"]["quiz_id"] = new_quiz.id

        return {
            "success": True,
            "data": result,
            "message": "Quiz restarted successfully",
        }

    except Exception as e:
        logger.error(f"Error restarting adaptive quiz: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error restarting adaptive quiz: {str(e)}",
        )
