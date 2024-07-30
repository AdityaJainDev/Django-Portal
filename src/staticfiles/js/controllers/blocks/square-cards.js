

export class SquareCards {
    constructor(el) {
        this.el = el;
        this.items = el.querySelectorAll('.square-cards__images');
        this.itemsActive = 'square-cards__images--active'
        this.initRollover();
        this.mobileDetection();
    }


    mobileDetection() {
        this.mediaObj = window.matchMedia('(max-width: 1023px)')
        return this.mediaObj.matches
    }


    // add resize behaviour here if needed
    onResize() {
    }

    initRollover() {

        this.items.forEach((slide, index) => {

            slide.addEventListener('mouseenter', (e) => {
                // console.log('mouseenter',this.mobileDetection(), slide)
                if (!this.mobileDetection()) {
                    slide.classList.add(this.itemsActive);
                }
            })
            slide.addEventListener('mouseleave', (e) => {
                // console.log('mouseenter',this.mobileDetection(), slide)
                if (!this.mobileDetection()) {
                    slide.classList.remove(this.itemsActive);
                }
            })
            slide.addEventListener('click', (e) => {
                if(this.mobileDetection()) {
                    this.items.forEach((slide) => {
                        slide.classList.remove(this.itemsActive)
                        // console.log(slide)
                    })
                    slide.classList.add(this.itemsActive)
                }
            })
        })
    }
}
