import { API_URL } from "./config.js";
import { postJson } from "./helper.js";

const form = document.querySelector("form");
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    try {
        const inputs = Array.from(this.querySelectorAll('.form__input'));
        const formData = {
            username:inputs[0].value,
            email:inputs[1].value,
            password:inputs[2].value
        }


        const data = await postJson(`${API_URL}/register/`,formData);
        if (data.error) throw new Error(data.error); 

        inputs.forEach(inp => inp.value = null);
        
        window.location.href ="./signin.html";



    } catch (error) {
        alert(error.message)
        console.error(error);
    }
    

})