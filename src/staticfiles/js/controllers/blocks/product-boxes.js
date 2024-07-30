
export class ProductBoxes {
    constructor(el) {
        this.el = el;
        this.products = el.querySelectorAll('.product-boxes__box');
        this.productActive = 'product-boxes__box--active'
        this.ctaHover = ('hover')
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

        this.products.forEach((box, index) => {

            box.addEventListener('mouseenter', (e) => {
               // console.log('mouseenter',this.mobileDetection(), box)
                if (!this.mobileDetection()) {
                    box.classList.add(this.productActive);
                    box.querySelector('.cta-btn').classList.add(this.ctaHover)
                }
            })
            box.addEventListener('mouseleave', (e) => {
                // console.log('mouseenter',this.mobileDetection(), box)
                if (!this.mobileDetection()) {
                    box.classList.remove(this.productActive);
                    box.querySelector('.cta-btn').classList.remove(this.ctaHover)
                }
            })
            box.addEventListener('click', (e) => {
                box.querySelector('.cta-btn').click()
                let a = box.querySelector('.cta-btn')
                console.log(a)
                if(this.mobileDetection()) {
                    this.products.forEach((box) => {
                        box.classList.remove(this.productActive)
                        // console.log(box)
                    })
                    box.classList.add(this.productActive)
                }
            })
        })
    }

}