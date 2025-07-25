// user input
export const MIN_NAME_LENGTH = 3
export const MAX_NAME_LENGTH = 25
export const MIN_EMAIL_LENGTH = 5
export const MAX_EMAIL_LENGTH = 254
export const MIN_PASSWORD_LENGTH = 8
export const MAX_PASSWORD_LENGTH = 20
export const OTP_EXACT_LENGTH = 6

// notes input
export const MIN_TITLE_LENGTH = 1
export const MAX_TITLE_LENGTH = 100
export const MIN_TEXT_LENGTH = 1
export const MAX_TEXT_LENGTH = 20000
export const MIN_PIN_LENGTH = 3
export const MAX_PIN_LENGTH = 8

// ======================================================================
// ========================== users validation ==========================
// ======================================================================

// Allows alphanumeric characters, underscores, spaces, and hyphens.
  // Content pattern check (no multiple spaces, allowed characters)
const nameContentRegex = /^[a-zA-Z0-9_\-]+(?:[ ][a-zA-Z0-9_\-]+)*$/

export const validateName = (name) => {
  // Length must be between 3 and 25 characters.
  if (typeof name !== 'string' || name.length < MIN_NAME_LENGTH || name.length > MAX_NAME_LENGTH) {
    return false
  }

  return nameContentRegex.test(name)
}

// =============================================================
// Follows a standard email format
// Does not allow leading/trailing spaces or spaces within the local part or domain.
// Content pattern check (standard email format, no spaces allowed by [^\s@])
const emailContentRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export const validateEmail = (email) => {
  // 5 to 254 char long
  if (typeof email !== 'string' || email.length < MIN_EMAIL_LENGTH || email.length > MAX_EMAIL_LENGTH) {
    return false
  }

  return emailContentRegex.test(email)
}

// ================================================================
// Requires at least one lowercase letter.
// Requires at least one uppercase letter.
// Requires at least one digit.
// Only allows alphanumeric characters.
const passwordContentRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]+$/

export const validatePassword = (password) => {
  // Length must be between 8 and 20 characters.
  if (typeof password !== 'string' || password.length < MIN_PASSWORD_LENGTH || password.length > MAX_PASSWORD_LENGTH) {
    return false
  }

  return passwordContentRegex.test(password)
}

// ================================================================
// Must consist of exactly 6 digits.
const otpContentRegex = /^\d+$/;

export const validateOtp = (otp) => {
  if (typeof otp !== 'string' || otp.length !== OTP_EXACT_LENGTH) {
    return false
  }

  return otpContentRegex.test(otp)
}


// ======================================================================
// ========================== notes validation ==========================
// ======================================================================

export const isValidTitle = (title) => {
  return title.length >= MIN_TITLE_LENGTH && title.length <= MAX_TITLE_LENGTH
}

export const isValidText = (text) => {
  return text.length >= MIN_TEXT_LENGTH && text.length <= MAX_TEXT_LENGTH
}

export const isValidPin = (pin) => {
  return pin.length >= MIN_PIN_LENGTH && pin.length <= MAX_PIN_LENGTH
}