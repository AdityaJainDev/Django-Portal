export class Faq {
  constructor() {
    let me = this;
    document.querySelectorAll('.single-faq__header').forEach(function(el) {
      me.initSingleFaq(el)
    })
  }

  initSingleFaq(el) {
    let me = this;
    el.addEventListener('click', function (e) {
      e.preventDefault()
      let el = e.target
      me.slideToggle(el.parentElement.querySelector('.single-faq__text'))
      el.parentElement.classList.toggle('opened')
    })
  }

  slideUp(target, duration=500) {

    target.style.transitionProperty = 'height, margin, padding';
    target.style.transitionDuration = duration + 'ms';
    target.style.boxSizing = 'border-box';
    target.style.height = target.offsetHeight + 'px';
    target.offsetHeight;
    target.style.overflow = 'hidden';
    target.style.height = 0;
    target.style.paddingTop = 0;
    target.style.paddingBottom = 0;
    target.style.marginTop = 0;
    target.style.marginBottom = 0;
    window.setTimeout( () => {
      target.style.display = 'none';
      target.style.removeProperty('height');
      target.style.removeProperty('padding-top');
      target.style.removeProperty('padding-bottom');
      target.style.removeProperty('margin-top');
      target.style.removeProperty('margin-bottom');
      target.style.removeProperty('overflow');
      target.style.removeProperty('transition-duration');
      target.style.removeProperty('transition-property');
      //alert("!");
    }, duration);
  }

  /* SLIDE DOWN */
  slideDown (target, duration=500) {

    target.style.removeProperty('display');
    let display = window.getComputedStyle(target).display;
    if (display === 'none') display = 'block';
    target.style.display = display;
    let height = target.offsetHeight;
    target.style.overflow = 'hidden';
    target.style.height = 0;
    target.style.paddingTop = 0;
    target.style.paddingBottom = 0;
    target.style.marginTop = 0;
    target.style.marginBottom = 0;
    target.offsetHeight;
    target.style.boxSizing = 'border-box';
    target.style.transitionProperty = "height, margin, padding";
    target.style.transitionDuration = duration + 'ms';
    target.style.height = height + 'px';
    target.style.removeProperty('padding-top');
    target.style.removeProperty('padding-bottom');
    target.style.removeProperty('margin-top');
    target.style.removeProperty('margin-bottom');
    window.setTimeout( () => {
      target.style.removeProperty('height');
      target.style.removeProperty('overflow');
      target.style.removeProperty('transition-duration');
      target.style.removeProperty('transition-property');
    }, duration);
  }

  /* TOOGLE */
  slideToggle (target, duration = 500) {
    if (window.getComputedStyle(target).display === 'none') {
      return this.slideDown(target, duration);
    } else {
      return this.slideUp(target, duration);
    }
  }
}