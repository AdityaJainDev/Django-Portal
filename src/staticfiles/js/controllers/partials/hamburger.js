

export class Hamburger {
    constructor(el) {
        this.el = el;
        this.headerDesktop = el.querySelector('.header__container')
        this.headerOnScroll = ('header__container--onScroll')
        this.hamburger = el.querySelector('.hamburger');
        this.hamburgerActive = ('is-active')
        this.list = el.querySelector('.header__list-mobile')
        this.listShow = ('header__list-mobile--show')
        this.addHamburger()
        this.onScroll()


    }

    addHamburger() {
        // console.log('here', this.body)
        this.hamburger.addEventListener('click', (e) => {
            // console.log('there', this.hamburger)
            this.hamburger.classList.toggle(this.hamburgerActive);
            this.list.classList.toggle(this.listShow)
            // console.log('here')
            document.body.classList.toggle('lockScroll')
        })
    }

    onScroll() {
        let lastKnownScrollPosition = 0;
        let ticking = false;
        let that = this;

        function doSomething(scrollPos) {
            if (scrollPos > 10) {
                that.headerDesktop.classList.add(that.headerOnScroll)
            }
            else {
                that.headerDesktop.classList.remove(that.headerOnScroll)
            }
        }

        document.addEventListener('scroll', function(e) {
            lastKnownScrollPosition = window.scrollY;

            if (!ticking) {
                window.requestAnimationFrame(function() {
                    doSomething(lastKnownScrollPosition);
                    ticking = false;
                });

                ticking = true;
            }
        });
    }


    // add resize behaviour here if needed
    onResize() {
    }
}
