class RoomCardsView {
    _parentEL = document.querySelector('.room-cards');

    handleBookBtnClicked(handler){
        this._parentEL.addEventListener('click', function(e){
            const bookBtn = e.target.closest('.room-card__btn');
            if(!bookBtn) return;
            handler(bookBtn.dataset.query);
        });
            
    }
}

export default new RoomCardsView();