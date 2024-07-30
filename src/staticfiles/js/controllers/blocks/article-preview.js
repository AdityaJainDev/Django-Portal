// core version + navigation, pagination modules:
import Swiper, { Navigation, Pagination } from 'swiper/core';

// configure Swiper to use modules
Swiper.use([Navigation, Pagination]);

export class ArticlePreview {
    constructor(el) {
        this.el = el;
        console.log('init')
        this.container = el.querySelector('.article-preview__container');
        this.images = el.querySelectorAll('.article-preview__images')

        this.mobileDetection();
        this.swiper = null;
        this.swiperClass = 'article-preview--swiper'
        this.initSwiper();

    }


    initSwiper() {
        if (this.swiper ) {
            this.swiper.destroy()
            this.swiper = null
        }
        this.swiperConfig = {
            loop: false,
            slidesPerView: 'auto',
            pagination: {
                el: ".swiper-pagination"
            },
            spaceBetween: 20
        }
        this.swiperConfigDesktop = {
            slidesPerView: 3,
            slidesPerGroup: 3,
            spaceBetween: 30,
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev'
            }
        }
        // console.log('here', this.fourImages);
        this.el.classList.remove(this.swiperClass)

        //se siamo su mobile inizializza lo swiper
        if(this.mediaObj.matches) {
            // console.log('here', this.images.length, this.container)
            this.el.classList.add(this.swiperClass)
            this.swiper = new Swiper( this.container, this.swiperConfig )
        }

        //se su desktop inizializza swiper solo se le news sono più di tre
        if(!this.mediaObj.matches )  {
             // console.log('here', this.images.length, this.container, this.el.querySelector('.swiper-button-next'))
            this.el.classList.add(this.swiperClass)
            this.swiper = new Swiper( this.container, this.swiperConfigDesktop )

        }
    }

    mobileDetection() {
        this.mediaObj = window.matchMedia('(max-width: 480px)')
    }


    // add resize behaviour here if needed
    onResize() {
        console.log("RESIZE ARTICLE PREVIEW")
        this.initSwiper();
    }
}
