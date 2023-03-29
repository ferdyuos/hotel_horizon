class SlideView{
    _parentEl = document.querySelector('.display-rooms');
    _slides  =  this._parentEl.querySelectorAll('.room-gallery');
    _dots  =  this._parentEl.querySelector('.dots');
    _curSlide = 0;

    _nextSlide(){
        if(++this._curSlide  === this._slides.length)
            this._curSlide = 0;
    }

    _prevSlide(){
        if(--this._curSlide  < 0)
            this._curSlide = this._slides.length - 1;
    }

    moveToSlideIndex(index){
        this._slides.forEach((s,i) => {
            s.style.transform = `translateX(${100  * ( i - this._curSlide)}%)`;
        })
    }

    _changeButtonStyle(btn = this._parentEl.querySelector('.btn-ctrl--left')){
        const btnLeft = this._parentEl.querySelector('.btn-ctrl--left');
        const btnRight = this._parentEl.querySelector('.btn-ctrl--right');

        switch (btn) {
            case btnLeft:
            case btnRight:
                if(this._curSlide === 0){
                    btnLeft.classList.add('btn-ctrl--inverted');
                    btnRight.classList.remove('btn-ctrl--inverted');

                }else if(this._curSlide > 0 && this._curSlide < this._slides.length -1){
                    btnLeft.classList.remove('btn-ctrl--inverted');
                    btnRight.classList.remove('btn-ctrl--inverted');
                }else{
                    btnRight.classList.add('btn-ctrl--inverted');
                    btnLeft.classList.remove('btn-ctrl--inverted');
                }
                break;
        }
    }



   

    handleSlideBtnClick(){
        this._parentEl.addEventListener('click', e =>{
            const btn = e.target.closest(".btn-ctrl");
            if(!btn) return;
            
            (btn.classList.contains('btn-ctrl--left')) ? this._prevSlide() : this._nextSlide();

           this.moveToSlideIndex(this._curSlide);
           this._changeButtonStyle(btn);

        })
    }
    
}

export default new SlideView();