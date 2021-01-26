import { Component, OnInit } from '@angular/core';

declare var $: any;

@Component({
  selector: 'app-select-word',
  templateUrl: './select-word.component.html',
  styleUrls: ['./select-word.component.scss']
})
export class SelectWordComponent implements OnInit {

  span: HTMLElement;
  word: string;
  checked: boolean;
  options: HTMLCollectionOf<Element>;
  option: string = '';
  optionsCount: number;
  wordLength: number;
  flipped: boolean;
  spanLeft: string;

  constructor() { }

  ngOnInit(): void {
    $('.text').lettering('words');
  }

  onClick(event: MouseEvent): void {
    let element = event.target as HTMLElement;
    this.option = '';
    this.flipped = false;

    if (element.className.startsWith('word')) {
      this.span = element;
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

    else if (element.nodeName.toLowerCase() === 'p') {
      setTimeout(() => {
        if (document.querySelector("#panel > div"))
          document.querySelector("#panel > div").setAttribute('style', 'display: none');
      }, 0);
    }
  }

  onShow(): void {
    let wordLength = this.wordLength;
    setTimeout(() => {
      let panelDiv = document.querySelector("#panel > div");
      if (panelDiv && this.span) {
        let panelX = panelDiv.getBoundingClientRect().left;
        let spanX = this.span.getBoundingClientRect().left;
        let optionsDiv = document.getElementsByClassName('options')[0];
        this.optionsCount = ((optionsDiv) ? optionsDiv.childElementCount : 0);

        // prevent panel from expanding past the bottom of the page after unchecking the checkbox by forcing it to face upwards initially
        if (this.span.getBoundingClientRect().top > 500 && !panelDiv.className.includes('flipped'))
            panelDiv.className = panelDiv.className + ' p-overlaypanel-flipped';
        
        // handle potential panel misalignment
        if (panelX-spanX != 0 || panelDiv.className.includes('flipped')) {
          let yOffset = 180 + this.optionsCount*28; // vertical offset for the upwards panel
          let x = ((wordLength > 3) ? this.span.offsetLeft : this.span.offsetLeft-15);
          let y: number;
          if (this.checked)
            y = ((panelDiv.className.includes('flipped')) ? this.span.offsetTop-95 : this.span.offsetTop+20);
          else
            y = ((panelDiv.className.includes('flipped')) ? this.span.offsetTop-yOffset : this.span.offsetTop+20);
          let top = y.toString();
          let left = x.toString();
          this.spanLeft = left;
          panelDiv.setAttribute('style', 'top: '+top+'px; left: '+left+'px; --overlayArrowLeft: 0px;');
        }
      }
    }, 0);
  }

  check(checked: boolean): void {
    this.checked = checked;
    this.option = '';

    // move the upwards panel to the word's location after (un)checking the checkbox
    if (this.flipped) {
      let wordLength = this.wordLength;
      setTimeout(() => {
        let panelDiv = document.querySelector("#panel > div");
        if (panelDiv && this.span) {
          let optionsDiv = document.getElementsByClassName('options')[0];
          this.optionsCount = ((optionsDiv) ? optionsDiv.childElementCount : 0);
          let x = ((wordLength > 3) ? this.span.offsetLeft : this.span.offsetLeft-15);
          let left = x.toString();
          let y: number
          let top: string;

          if (this.checked)
            y = ((panelDiv.className.includes('flipped')) ? this.span.offsetTop-95 : this.span.offsetTop+20);
          else {
            let yOffset = 180 + this.optionsCount*28; // vertical offset for the upwards panel
            y = ((panelDiv.className.includes('flipped')) ? this.span.offsetTop-yOffset : this.span.offsetTop+20);
          }

          top = y.toString();
          panelDiv.setAttribute('style', 'top: '+top+'px; left: '+left+'px; --overlayArrowLeft: 0px;');
        }
      }, 0);
    }
  }
}
