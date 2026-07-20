import axios from "axios";

class SpamshieldMethods{
    constructor(){
        this.backendUrl = "http://127.0.0.1:8000"
        this.regexes = []
        
        
        this.getRegexes()
    }
    addRegex(newRegex){
        let regex = document.querySelector('#input-add-regex').value
        axios.post(`${this.backendUrl}/new-regex`, newRegex)
        .then(response => {
            console.log(response.data)
        })
        .catch(error => {
            console.error(error)
            alert(error)
        })
        
    }

    getRegexes(){
        axios.get(`${this.backendUrl}/get-regexes`)
        .then(response => {
            this.regexes = response.data
            console.log(response.data)
        })
        .catch(error => {
            console.error(error)
            alert(error)
        })
    }

    deleteRegex(id){
        axios.delete(`${this.backendUrl}/delete-regex/${id}`)
        .then(response => {
            console.log(response.data)
            this.getRegexes()
        })
        .catch(error => {
            console.error(error)
            alert(error)
        })
    }

}


SPMSLD = new SpamshieldMethods()
