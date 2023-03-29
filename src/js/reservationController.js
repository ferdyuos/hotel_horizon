import * as model from "./model.js";
import reserveView from "./views/reserveView.js";


const controlLoadReservation =  async function() {
    try {
        await model.loadHotels();

        
        const param = new URLSearchParams(window.location.search);
        const city = param.get('query');

        reserveView.updateName(city);

    } catch (error) {
        console.error(error);
    }
}

const goToPreviousPage = function(){
    history.back();
}

const controlBookRoom = async function(arrayData){
   try {
       const param = new URLSearchParams(window.location.search);
        const city = param.get('query');

        const [currentHotel] = model.state.hotels.filter(hotel => hotel.city.toLowerCase() === city.toLowerCase());

        if(!currentHotel) throw new Error('No such Hotel');

       const[date, type, number_people] = arrayData;
       const bookingData = {
           user_id: sessionStorage?.getItem("userID"),
           id:currentHotel?.id,
           type,
           date: new Date(date).toISOString(),
           number_people
       }


       
       const result = await model.bookHotel(bookingData);
       sessionStorage.setItem("bookingResponse", JSON.stringify(result));
       window.location.href = "./payment.html";
   } catch (error) {
        console.error(error);    
   }
}






const init = function () {
    reserveView.handleFormRoomTypeChange();
    // reserveView.handleCheckInDateChanged();
    reserveView.handleBackBtnClick(goToPreviousPage);
    reserveView.handleSubmitBtnClick(controlBookRoom);
}

init();



window.addEventListener('load', controlLoadReservation);
window.addEventListener('load', reserveView.handleSetMaxBookingDate);