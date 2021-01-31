import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

declare var $: any;

@Component({
  selector: 'app-select-word',
  templateUrl: './select-word.component.html',
  styleUrls: ['./select-word.component.scss']
})
export class SelectWordComponent implements OnInit {

  span: HTMLElement;
  spanX: number;
  spanY: number;
  word: string;
  checked: boolean;
  options: HTMLCollectionOf<Element>;
  option: string = '';
  optionsCount: number;
  wordLength: number;
  flipped: boolean;

  constructor(private router: Router) { }

  ngOnInit(): void {
    $('.text').lettering('words');
  }

  onClick(event: MouseEvent): void {
    let element = event.target as HTMLElement;
    this.option = '';
    this.flipped = false;

    if (element.className.startsWith('word')) {
      this.span = element;
      this.spanX = element.offsetLeft;
      this.spanY = element.offsetTop;
      this.word = this.span.textContent.replace(/[^\p{L}\s]/gu,""); // remove punctuation
      this.wordLength = this.word.length;
      setTimeout(() => {
        let panelDiv = document.querySelector("#panel > div");
        if (panelDiv && panelDiv.className.includes('flipped'))
          this.flipped = true;
      }, 100);
    }
    
    // panel option selection
    else if (element.className === 'option') {
      this.option = element.textContent;
      this.options = document.getElementsByClassName('option');
      
      for (let i=0; i<this.options.length; i++) {
        let opt = this.options[i];
        if (opt.getAttribute('style') == null)
          opt.setAttribute('style', 'background: white');
        if (opt.textContent === element.textContent) {
          if (opt.getAttribute('style').includes('#')) { // deselect
            this.option = '';
            opt.setAttribute('style', 'background: white; font-weight: initial');
          }
          else
            opt.setAttribute('style', 'background: #DAEBF9; font-weight: 500')
        }
        else
          opt.setAttribute('style', 'background: white; font-weight: initial');
      }
    }

    // prevent the panel from showing after clicking on empty space between words
    else if (element.nodeName.toLowerCase() === 'p') {
      setTimeout(() => {
        if (document.querySelector("#panel > div"))
          document.querySelector("#panel > div").setAttribute('style', 'display: none');
      }, 0);
    }
  }

  onShow(): void {
    setTimeout(() => {
      this.movePanel(true);
    }, 0);
  }

  check(checked: boolean): void {
    this.checked = checked;
    this.option = '';

    // move the upwards panel to the word's location after (un)checking the checkbox
    if (this.flipped) {
      setTimeout(() => {
        this.movePanel(false);
      }, 0);
    }
  }

  // handle potential misalignment of the panel
  movePanel(onShow: boolean): void {
    let panelDiv = document.querySelector("#panel > div");

    if (panelDiv && this.span) {
      let optionsDiv = document.getElementsByClassName('options')[0];
      this.optionsCount = optionsDiv ? optionsDiv.childElementCount : 0;

      // prevent the panel from expanding past the bottom of the page after unchecking the checkbox by forcing it to face upwards initially
      if (onShow && this.span.getBoundingClientRect().top > 500 && !panelDiv.className.includes('flipped'))
        panelDiv.className = panelDiv.className + ' p-overlaypanel-flipped';
      
      let x = (this.wordLength > 3) ? this.spanX : this.spanX-15;
      let y: number;
      if (this.checked)
        y = panelDiv.className.includes('flipped') ? this.spanY-95 : this.spanY+20;
      else {
        let yOffset = 180 + this.optionsCount*28; // vertical offset for the upwards panel
        y = panelDiv.className.includes('flipped') ? this.spanY-yOffset : this.spanY+20;
      }

      let top = y.toString();
      let left = x.toString();
      panelDiv.setAttribute('style', 'top: '+top+'px; left: '+left+'px; --overlayArrowLeft: 0px;');
    }
  }

  addDescription(): void {
    if (this.option === '')
      this.router.navigate(['/rec']);
    // TODO else: anotiraj prema izabranoj opciji
  }

  changeDescription(): void {
    let word = this.option.split(' - ')[0].split(') ')[1];
    this.router.navigate(['/rec/'+word]);
  }
}
