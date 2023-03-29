import * as model from "./model.js";
import resultsView from "./views/resultsView.js";

const controlRenderSearch = async function(){
    try {
        resultsView.renderSpinner();
        await model.loadHotels();
        resultsView.render(model.state.hotels);
        
    } catch (error) {
        console.error(error);
    }
}

const controlSearchRoom = function(data){
  if (!Object.values(data).some(data => data)) return; 
    model.makeSearch(data);
    resultsView.render(model.state.search);
}

const controlBookBtnClick = function(queryParam){
    window.location.assign(`./reservation.html${queryParam}`);
}

const init = function () {
    resultsView.handleHotelRoomSearch(controlSearchRoom);
    resultsView.handleBookBtnClicked(controlBookBtnClick);
}
init();
window.addEventListener('load',controlRenderSearch);