import { API_GET_CONFIG, API_POST_CONFIG, TIME_OUT_SEC } from "./config.js";

const wait = function(sec){
    return new Promise(function(_, reject){
        setTimeout(() => {
            reject(new Error('Request took too long'));
        }, sec * 1000);
    })
}

export const getJson = async function(url){
    try {
        const req =  await Promise.race([
            fetch(url,API_GET_CONFIG),
            wait(TIME_OUT_SEC)
        ]);

        const data = await req.json();
        if(!data)  throw new Error('no data to json');

        return data;
    }catch(error){
        console.log(error);
        throw error;
    }
}


export const postJson = async function(url, formData){
    try {
        API_POST_CONFIG.body = JSON.stringify(formData);
        
        const req =  await Promise.race([
            fetch(url,API_POST_CONFIG),
            wait(TIME_OUT_SEC)
        ]);

        const data = await req.json();
        if(!data) throw new Error('no data to json');

        return data;
    }catch(error){
        console.error(error);
        throw error;
    }
}