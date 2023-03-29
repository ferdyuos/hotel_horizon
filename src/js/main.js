import searchView from "./views/SearchView.js";
import slideView from "./views/slideView.js";
import * as model from "./model.js";
import roomCardsView from "./views/roomCardsView.js";

const controlLoadHotelsOnStart = async function(){
    try {
        await model.loadHotels();
    } catch (error) {
        console.error(error)
    }
}


const controlStickyNav = function(){
    const hero = document.querySelector('.hero');
    const nav = document.querySelector('.header');
    const navHeight = nav.getBoundingClientRect().height;

    const stickyNav = function(entries){
        const [entry] = entries;

        if(!entry.isIntersecting)
            nav.classList.add('sticky');
        else
            nav.classList.remove('sticky');
    }

    const options = {
        root:null,
        threshold:0,
        rootMargin: `-${navHeight}px`
    }

    const headerObserver = new IntersectionObserver(stickyNav,options);
    headerObserver.observe(hero);
}


const controlDisplayDropdown = function(){
    searchView.render(model.state.hotels)
}

const controlSearchBtnClicked =  function(){

}

const controlBookBtnClick = function(queryParam){
    window.location.assign(`./src/pages/reservation.html${queryParam}`);
}



const init = function(){
controlLoadHotelsOnStart();
    controlStickyNav();
    slideView.handleSlideBtnClick();
    slideView.moveToSlideIndex(0);
    searchView.searchDropdownClickHandler(controlDisplayDropdown);
    searchView.handleSearchBtnClick(controlSearchBtnClicked);
    roomCardsView.handleBookBtnClicked(controlBookBtnClick);
}


init();