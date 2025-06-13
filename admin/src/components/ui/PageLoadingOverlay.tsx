import React from 'react'

const PageLoadingOverlay = () => {
    return (
        <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
    )
}

export default PageLoadingOverlay