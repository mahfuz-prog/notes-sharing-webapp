import { reactive, readonly } from "vue"

import config from "../config.json"

const authState = reactive({
	token: localStorage.getItem('token'),
	SERVER_ADDR: config.SERVER_ADDR,
	FRONTEND: config.FRONTEND,
	username: localStorage.getItem('username')
})

// --- Auth Actions Object ---
const authActions = {
    updateToken(token) {
        authState.token = token
        localStorage.setItem('token', token)
    },

    getAuthorizationHeader() {
        return { 'Authorization': `${config.AUTH_PREFIX} ${authState.token}` }
    },

    resetAuth() {
        authState.token = null
        localStorage.removeItem('token')
    }, 

    setUsername(name) {
    	authState.username = name
    	localStorage.setItem('username', name)
    }
}


// notes ==============================================
// pagination = { "currentPage": "", "hasPrev": "", "hasNext": "", "pageList": [] } 
// notes = { {'id': "", 'info': {'title':"", 'dateCreated': "", 'text': "", 'pin': ""}}, }
const notesState = reactive({
	pagination: {},
	noteList: new Map()	   // ordered map
})


const notesStateActions = {
	// set all notes
	setNotes(data) {
		// first reset
		notesStateActions.resetNotes()

		notesState.pagination = data.pagination
		data.notes.forEach(note => {
            notesState.noteList.set(note.id, note.info)
        })
	},

	// delete note
	deleteNote(id) {
        const newNotesMap = new Map(notesState.noteList)
        newNotesMap.delete(id)
        notesState.noteList = newNotesMap
	},

	// update note
	updateNote(id, title, text, pin) {
        const updatedInfo = {
            'dateCreated': notesState.noteList.get(id).dateCreated,
            'pin': pin,
            'text': text,
            'title': title
        }

        // Create a new Map based on the old one
        const newNotesMap = new Map(notesState.noteList)
        newNotesMap.set(id, updatedInfo)
        notesState.noteList = newNotesMap
	},

	setNewNote(id, title, text, pin) {
	    const currentNotesArray = Array.from(notesState.noteList.entries())

	    // 1. Remove the last element if the list is not empty
	    if (currentNotesArray.length > 5) {
	      currentNotesArray.pop()
	    }

        const noteInfo = { 'pin': pin, 'text': text, 'title': title }
	    const updatedNotesArray = [ [id, noteInfo], ...currentNotesArray ]
	    notesState.noteList = new Map(updatedNotesArray)
	},

	// reset
    resetNotes() {
        notesState.pagination = {}
        notesState.noteList.clear()
    }
}


// active note
const activeNoteState = reactive({
	id: "",
	title: "",
	text: "",
	dateCreated: "",
	pin: "",
})

const activeNoteActions = {
	setActiveNote(id, title, text, dateCreated, pin) {
		activeNoteState.id = id
		activeNoteState.title = title
		activeNoteState.text = text
		activeNoteState.dateCreated = dateCreated
		activeNoteState.pin = pin

		// when select a note for active create a temp for this note
		tempNoteActions.setTemp(title, text, pin)
	},

	clearActiveNote() {
		activeNoteState.id = ""
		activeNoteState.title = ""
		activeNoteState.text = ""
		activeNoteState.dateCreated = ""
		activeNoteState.pin = ""
	}
}


// temporary notes
const tempNoteState = reactive({
    title: "",
    text: "",
    pin: "",
})

const tempNoteActions = {
	// reset
	setTemp(title, text, pin) {
		tempNoteState.title = title
		tempNoteState.text = text
		tempNoteState.pin = pin
	},

	// edit title
	editTitle(title) {
		tempNoteState.title = title
	},

	// edit text
	editText(text) {
		tempNoteState.text = text
	},

	// edit pin
	editPin(pin) {
		tempNoteState.pin = pin
	},

	// get note edited status
	get isEdited() {
		if (
			activeNoteState.title != tempNoteState.title || 
			activeNoteState.text != tempNoteState.text || 
			activeNoteState.pin != tempNoteState.pin) {
			return true
		} else {
			return false
		}
	}
}



export default {
	authState: readonly(authState),
	authActions,

	notesState: readonly(notesState),
	notesStateActions,

	tempNoteState: readonly(tempNoteState),
	tempNoteActions,

	activeNoteState: readonly(activeNoteState),
	activeNoteActions
}