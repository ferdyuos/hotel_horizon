export const API_URL = "http://localhost:5000/api";
export const TIME_OUT_SEC = 15;
export const API_POST_CONFIG = {
    method: 'POST',
    headers:{
        'Authorization' : `Basic ${btoa('admin:admin')}`,
        'Content-Type': 'application/json; charset=utf-8',
    }, 
    body:''
}

export const API_GET_CONFIG = {
    method: 'GET',
    headers:{
        Accept: 'application/json;',
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization' : `Basic ${btoa('admin:admin')}`,
    }
}