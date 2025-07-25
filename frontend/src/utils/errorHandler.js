import axios from "axios"

// used in skeleton loading views component
export function viewErrorHandler({ store, router, errorRef }) {
	// The returned function will be the actual handler for onErrorCaptured
	return (err) => {
	  // This is an error originating from an Axios HTTP request
	  if (axios.isAxiosError(err)) {
	    // The server responded with an error status
	    if (err.response) {
	      if (err.response.status === 401 || err.response.status === 403) {
	        store.authActions.resetAuth()
	        router.push({ name: "login" })
	        return false
	      }

	      // Check for specific error message from the backend response data
	      if (err.response.data && err.response.data.error) {
	        errorRef.value = err.response.data.error
	        return false
	      }

	      // Fallback for server errors if no specific message in data.error
	      errorRef.value = `Server Error: ${err.response.status}`
	      return false

	    } else if (err.request) {
	      // The request was made but no response was received (e.g., no internet, backend offline)
	      errorRef.value = "It looks like you're offline or the server is unavailable."
	      return false
	    }
	  } else {
	    // This branch catches general JavaScript runtime errors
	    // (e.g., TypeError, ReferenceError, or custom Error objects)
	    errorRef.value = "An unknown error occurred."
	    return false
	  }
	}
}