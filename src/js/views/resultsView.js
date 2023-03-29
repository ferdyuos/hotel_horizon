import images from 'url:./../../images/*.jpg';
class ResultsView {
    _parentEl = document.querySelector('.results');
    _data;
    

    render(data){
        if(!data) return;
        this._data = data;
        const markup = this._generateMarkup();
        this._parentEl.innerHTML = null;
        this._parentEl.innerHTML = markup;


    }

    renderSpinner(){
        const markup = `
             <div class="loader">
                <svg version="1.1" id="loader-1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                   width="70px" height="70px" viewBox="0 0 50 50" style="enable-background:new 0 0 50 50;" xml:space="preserve">
                <path fill="#000" d="M25.251,6.461c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615V6.461z">
                  <animateTransform attributeType="xml"
                    attributeName="transform"
                    type="rotate"
                    from="0 25 25"
                    to="360 25 25"
                    dur="0.6s"
                    repeatCount="indefinite"/>
                  </path>
                </svg>
              </div>
        `;
        this._parentEl.innerHTML = null;
        this._parentEl.innerHTML = markup;
    }
    _generateMarkup(){
        return this._data.map(this._generateMarkupPreview).join("");
    }

    _generateMarkupPreview(result){
         const random = Math.floor(Math.random() * 5) + 1;
         const name =`room-${random}`;
        return `
          <figure class="result">
                <img src="${images[name]}" alt="result image" class="result__img">
                <div class="result__desc">
                    <small class="result__location">${result.city}</small>
                    <button data-query="?query=${result.city}" class="btn">Book</button>
                </div>
            </figure>
        `;
    }

    handleHotelRoomSearch(handler){
        document.querySelector('.search-form').addEventListener('submit',function(e) {
            e.preventDefault();
            const inputs = Array.from(this.querySelectorAll('.form__input'));
            
             const formData = {
                city:(inputs[0].value.trim() === '') ? null : inputs[0].value.toLowerCase(),
                capacity:(inputs[1].value === 'Capacity') ? null : +inputs[1].value,
                price:(inputs[2].value.trim() === '') ? null : +inputs[2].value
            }
            this.reset();
            handler(formData);
        })
    }

    handleBookBtnClicked(handler){
        this._parentEl.addEventListener('click',function(e){
            const bookBtn = e.target.closest('.btn');
            if(!bookBtn) return;
            handler(bookBtn.dataset.query);
        })
    }
}

export default new ResultsView();