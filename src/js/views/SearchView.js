class SearchView{
    _parentEl = document.querySelector('.search');
    _dropdown = this._parentEl.querySelector('.dropdown');
    _subEl;

    _data;
    _target;
    _searchData;

    

    _generateMarkup(){
        const unique = this._data
                .map(hotel => hotel[this._searchData]);


        return ['Select',...new Set(unique)]
                .map(this._generateMarkupPreview).join("");
    }

    _generateMarkupPreview(result){
        return  `
            <li class="dropdown__item">${result}</li>
        `;
    }

    removeDropdown(){
        this._dropdown.classList.add('hidden');
    }

    render(data){
        if(!data) return;
        this._data = data;
        const markup = this._generateMarkup(data);
        this._dropdown.innerHTML = null;
        this._dropdown.innerHTML = markup;
        this._dropdown.classList.remove('hidden');
    }

    _resetSearchFields(){
        document.querySelectorAll('.search__detail')
        .forEach(el => el.textContent = 'Select');

    }

    handleSearchBtnClick(){
        this._parentEl.addEventListener('click', e => {
            const searchBtn = e.target.closest('.search__btn');
            if(!searchBtn) return;

            this._resetSearchFields();
        });

    }


    searchDropdownClickHandler(handler){
        document.addEventListener('click',e =>{
           this._target = e.target.closest('.search__title');
            if(!this._target){
               const dropdownItem = e.target.closest('.dropdown__item');

               if(dropdownItem){
                   
                this._subEl.textContent =  dropdownItem.textContent;
               }
                this.removeDropdown();
                return;
            }
            this._searchData = this._target.dataset.search;
            this._subEl =  this._target.parentElement.querySelector('.search__detail');

            handler();
        });
    }
    
}

export default new SearchView();