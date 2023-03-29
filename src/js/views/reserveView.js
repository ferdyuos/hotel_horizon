class ReserveView{
    _parentEl = document.querySelector('.reservation');
    _form =  this._parentEl.querySelector('.reservation__form');
    _self = this;


    updateName(name){
        this._parentEl.querySelector('.hotel').textContent = name;
    }

    handleBackBtnClick(handler){
        this._parentEl.addEventListener('click', e => {
            const backBtn = e.target.closest('.btn-back');
            if(!backBtn) return;
            handler();
        })
    }

    handleFormRoomTypeChange(){
        const roomMaxPeople = {
            standard: 1,
            double: 2,
            family: 6
        }
        const parent = this._parentEl;
        this._form.querySelector("#room-type").addEventListener('change',function(){
            parent.querySelector('#num-guest').setAttribute('max',roomMaxPeople[this.value.toLowerCase()]);
        })
    }

    handleCheckInDateChanged(){
        this._form.querySelector('#check-in').addEventListener('change',this.handleSetMaxBookingDate);
    }

    handleSetMaxBookingDate(){
        const checkInInput = document.querySelector('#check-in');
        const now = new Date(Date.now());
        const threeMonthsAway = new Date()

        threeMonthsAway.setMonth(now.getMonth() + 3);
        threeMonthsAway.setDate(now.getDate());

        
        const min = now.toISOString().split('.')[0].slice(0,-3);
        const max = new Date(threeMonthsAway).toISOString().split('.')[0].slice(0,-3);

        
        
        checkInInput.min = min;
        checkInInput.max = max;
       
    }

    handleSubmitBtnClick(handler){
        this._form.addEventListener('submit', function(e) {
            e.preventDefault();
            const inputs = Array.from(this.querySelectorAll('.form__input'));
            const values = inputs.map(inp => inp.value.toLowerCase());
            handler(values);
            this.reset();
        })
    }
}


export default new ReserveView();