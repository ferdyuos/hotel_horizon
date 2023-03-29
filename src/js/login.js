import { API_URL } from "./config.js";
import { postJson } from "./helper.js";
import * as model from './model.js';

const form = document.querySelector("form");
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    try {
        const inputs = Array.from(this.querySelectorAll('.form__input'));
        const formData = {
            email:inputs[0].value,
            password:inputs[1].value
        }


        const data = await postJson(`${API_URL}/login/`,formData);
        if (data.error) throw new Error(data.error); 


        window.location.href ="./search-results.html";
        sessionStorage.setItem('userID',data.id);

        inputs.forEach(inp => inp.value = null);
    } catch (error) {
        alert(error.message)
        console.error(error);
    }
    

})