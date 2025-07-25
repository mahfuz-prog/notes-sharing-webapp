// copy functionality
export function copyToClipboard (text) {
  // Check for modern clipboard API support
  if (navigator.clipboard) {
    return navigator.clipboard.writeText(text)
  } else {
    // Fallback for older browsers
    return new Promise((resolve, reject) => {
      const textArea = document.createElement('textarea')
      textArea.value = text
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()

      try {
        document.execCommand('copy')
        resolve()
      } catch (err) {
        reject(err)
      }

      document.body.removeChild(textArea)
    })
  }
}
