import * as model from "./model.js";
import bookingsView from "./views/bookingsView.js";

const controlLoadBookings = async function(){
    try {
        const userID = sessionStorage.getItem("userID");
        const payLoad = { id:userID };
        await model.loadBookings(payLoad);
        bookingsView.render(model.state.bookings.reverse());
        // console.log(model.state.bookings.reverse());

    } catch (error) {
        console.error(error);
    }
}

const controlDeleteBooking = async function(id){
    try {
        const data = {id};
        const {message} = await model.deleteBooking(data);
        await controlLoadBookings();
        alert(message);
    } catch (error) {
        console.error(error);
    }
}

const init = function(){
    bookingsView.handleDelBtnClick(controlDeleteBooking);
}

init();


window.addEventListener('load',controlLoadBookings);