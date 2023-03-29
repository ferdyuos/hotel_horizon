import icon from 'url:./../../images/icon/sprite.svg';

class BookingsView {
    _parentEL =  document.querySelector(".bookings__table");
    _data;

    render(data){
        this._data = data;
        const markUp = this._generateMarkup();
        this._clear();
        this._parentEL.innerHTML = markUp;
    }

    _clear(){
        this._parentEL.innerHTML = null;
    }

    _generateMarkup(){

        return `
            <tr>
                <th>#</th>
                <th>City</th>
                <th>Ref Code</th>
                <th>Status</th>
                <th></th>
            </tr>
        `+ this._data.map(this._generateMarkupPreview).join('');
    }
    _generateMarkupPreview(result,idx){
        return `
                <tr>
                <td>${idx+1}</td>
                <td>${result.city}</td>
                <td>${result.ref_code}</td>
                <td>${result.status}</td>
                <td>
                    <button class="bookings__del-btn" data-id="${result.id}">
                        <svg class="bookings__icon">
                            <use xlink:href="${icon}#icon-trash"></use> 
                        </svg>
                    </button>
                </td>
            </tr>
        `;
    }
    handleDelBtnClick(handler){
        this._parentEL.addEventListener('click',function(e){
            const delBtn = e.target.closest('.bookings__del-btn');
            if(!delBtn) return;
            const {id} = delBtn.dataset;
            handler(id);
        })
    }

}

export default new BookingsView();