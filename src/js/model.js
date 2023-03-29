import { API_URL } from "./config";
import { getJson, postJson } from "./helper.js";

class Hotel {

    constructor({id,city, capacity, peak_rate, off_peak_rate}){
        this.id = id;
        this.city = city;
        this.capacity = capacity;
        this.peak_rate = peak_rate;
        this.off_peak_rate = off_peak_rate;
        this.price = this._getPrice();
    }


    _getPrice(){
        const currentMonth = new Date().getMonth();
        return (currentMonth > 2  && currentMonth < 9) ? this.peak_rate : this.off_peak_rate;
    }

}

export const state = {
    hotels : [],
    search:[],
    bookings:[],
    currentSlide:0,
}

export const makeSearch = function({city, price, capacity}){
    const result = [];

    
    state.hotels.forEach(hotel => {
       if(hotel.city.toLowerCase().includes(city)){
           result.push(hotel);
       }
       if(price && hotel.price >= price) {
           result.push(hotel);
       }

       if(capacity && hotel.capacity === capacity) {
           result.push(hotel);
       }
    })

   state.search = [...new Set(result)];
}

export const bookHotel = async function(formData){
    try {
        const data = await postJson(`${API_URL}/book/`,formData);
        return data;
    } catch (error) {
        console.log(error);
        throw error;
    }
}

export const loadHotels = async function(){
    try {
        const data = await getJson(`${API_URL}/hotel-listings/`);
        state.hotels = data.map(obj => new Hotel(obj));
    } catch (error) {
        console.error(error);
        throw error;
    }

}

export const loadBookings = async function (data){
    try {
        const resp = await postJson(`${API_URL}/my-bookings/`,data);
        state.bookings = resp;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export const deleteBooking =  async function (data){
    try{
        const resp = await postJson(`${API_URL}/cancel-booking/`,data);
        console.log(resp );
        
        return resp;
    }catch(error){
        console.error(error);
        throw error;
    }
}

export const makePayment = async function(){
    try {
        const paymentBody = {
            booking_id: JSON.parse(sessionStorage.getItem("bookingResponse"))?.id,
            user_id: sessionStorage.getItem("userID")
        }

        const data = await postJson(`${API_URL}/payment/`,paymentBody);

        return data;

    } catch (error) {
        console.error(error);
        throw error;
    }
}

