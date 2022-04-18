import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { PublikacijaService } from '../../services/publikacije/publikacija.service';
import { SearchService } from '../../services/search/search.service';
import { OverlayPanel } from 'primeng/overlaypanel';

interface Option {
  word: string;
  type: string;
  id: number;
  type_id: number;
}

@Component({
  selector: 'app-pub-text',
  templateUrl: './pub-text.component.html',
  styleUrls: ['./pub-text.component.scss']
})
export class PubTextComponent implements OnInit, OnDestroy {

  pub: any;
  pubId: number;
  fragmentNr: number;
  title: SafeHtml;
  paragraphs: SafeHtml[];
  dirty: boolean;
  saveTimerId: any;

  span: HTMLElement;
  optionsCount: number;
  spanX: number;
  spanY: number;
  wordLength: number;
  flipped: boolean;
  checked: boolean;
  word: string;
  option: string;
  options: Option[];
  wordTypesMap: any;
  clickedWord: HTMLElement;
  selectedWordId: number;
  selectedWordTypeId: number;
  @ViewChild(OverlayPanel) panel: OverlayPanel;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private domSanitizer: DomSanitizer,
    private publikacijaService: PublikacijaService,
    private searchService: SearchService,
  ) {
    this.pub = {};
    this.paragraphs = [];
    // this.wordTypesMap = {
    //   именица: 'imenica',
    //   глагол: 'glagol',
    //   придев: 'pridev',
    //   заменица: 'zamenica',
    //   број: 'broj',
    //   прилог: 'prilog',
    //   предлог: 'predlog',
    //   узвик: 'uzvik',
    //   речца: 'recca',
    //   везник: 'veznik'
    // };
    this.wordTypesMap = {
      0: 'imenica',
      1: 'glagol',
      2: 'pridev',
      3: 'zamenica',
      4: 'broj',
      5: 'prilog',
      6: 'predlog',
      7: 'uzvik',
      8: 'recca',
      9: 'veznik'
    };
    this.option = '';
  }

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      this.pubId = +params.pid;
      this.fragmentNr = +params.fid;
      this.publikacijaService.get(this.pubId).subscribe((value) => {
        this.pub = value;
        this.title = this.publikacijaService.getOpis(this.pub);
        this.pub.autori = this.pub.autor_set.map((item, index) => ({ index, ime: item.ime, prezime: item.prezime}));
        this.pub.vrsta = this.publikacijaService.getPubType(this.pub.vrsta?.id);
        delete this.pub.autor_set;
        this.publikacijaService.getFragment(this.pubId, this.fragmentNr).subscribe(
          (tekst) => {
            this.paragraphs = this.split(tekst.tagovan_tekst);
            this.route.queryParams.subscribe((queryParams) => {
              // TODO: parametri za povratak iz forme za dodavanje nove lekseme
            });
          },
          (error) => {
            console.log(error);
          });
      });
    });
    this.dirty = false;
    this.saveTimerId = setInterval(() => { this.updateTaggedText(); }, 5000);
  }

  ngOnDestroy(): void {
    clearInterval(this.saveTimerId);
  }

  next(): void {
    this.router.navigate(['/publikacija', this.pubId, 'fragment', this.fragmentNr + 1]);
  }

  prev(): void {
    if (this.fragmentNr > 1)
      this.router.navigate(['/publikacija', this.pubId, 'fragment', this.fragmentNr - 1]);
  }

  click(event: MouseEvent): void {
    const element = event.target as HTMLElement;
    this.option = '';
    this.flipped = false;
    if (element.className.startsWith('word')) {
      this.checked = (element.classList.contains('ignore'));
      this.selectedWordId = element.getAttribute('data-id') ? +element.getAttribute('data-id') : null;
      this.selectedWordTypeId = element.getAttribute('data-typeid') ? +element.getAttribute('data-typeid') : null;
      this.clickedWord = element;
      this.span = element;
      this.spanX = element.offsetLeft;
      this.spanY = element.offsetTop;
      this.word = this.span.textContent.replace(/[^\p{L}\s]/gu, ''); // remove punctuation
      this.wordLength = this.word.length;
      this.searchService.searchWords(this.word).subscribe(
        (data) => {
          this.options = data.map((item) => ({word: item.rec, type: item.vrsta_text, type_id: item.vrsta, id: item.pk}));
          setTimeout(() => {
            const panelDiv = document.querySelector('#panel > div');
            if (panelDiv && panelDiv.className.includes('flipped'))
              this.flipped = true;
          }, 100);
        },
        (error) => console.log(error));
    }

    // panel option selection
    else if (element.className.includes('option ')) {
      console.log(element);
      this.option = element.textContent;
      const allOptions = document.getElementsByClassName('option');

      for (let i = 0;  i < allOptions.length; i++) {
        const opt = allOptions[i];
        if (opt.getAttribute('style') == null)
          opt.setAttribute('style', 'background: white');
        if (opt.textContent === element.textContent) {
          if (opt.getAttribute('style').includes('#')) { // deselect
            this.option = '';
            opt.setAttribute('style', 'background: white; font-weight: initial');
            this.span.classList.add('untagged');
          }
          else {
            opt.setAttribute('style', 'background: #DAEBF9; font-weight: 800');
            this.span.classList.remove('untagged');
          }
          // console.log(this.join(this.paragraphs));
          // this.publikacijaService.updateFragment(this.pubId, this.fragmentNr, this.join(this.paragraphs)).subscribe(
          //   (data) => {}, (error) => console.log(error));
        }
        else
          opt.setAttribute('style', 'background: white; font-weight: initial');
      }

      // setTimeout(() => {
      //   const panelDiv = document.querySelector('#panel > div');
      //   if (panelDiv && panelDiv.className.includes('flipped'))
      //     this.flipped = true;
      // }, 100);
    }

    // handle a click between the options
    else if (element.className === 'options') {
      this.option = '';
      const allOptions = document.getElementsByClassName('option');
      for (let i = 0; i < allOptions.length; i++) {
        const opt = allOptions[i];
        const style = opt.getAttribute('style');
        if (style && style.includes('#')) // deselect
          opt.setAttribute('style', 'background: white; font-weight: initial');
      }
      setTimeout(() => {
        const panelDiv = document.querySelector('#panel > div');
        if (panelDiv && panelDiv.className.includes('flipped'))
          this.flipped = true;
      }, 100);
    }

    // prevent the panel from showing after clicking on empty space between words
    else if (element.nodeName.toLowerCase() === 'p') {
      setTimeout(() => {
        if (document.querySelector('#panel > div'))
          document.querySelector('#panel > div').setAttribute('style', 'display: none');
      }, 0);
    }
  }

  split(text: string): SafeHtml[] {
    const retval: SafeHtml[] = [];
    const paras = text.split('\n');
    for (const para of paras) {
      // const words = para.split(' ');
      // const tagged = words.map((word, index) => `<span class="word word${index + 1} untagged">${word}</span>`);
      const finalText = this.domSanitizer.bypassSecurityTrustHtml(para);
      retval.push(finalText);
    }
    return retval;
  }

  join(paras: SafeHtml[]): string {
    return paras.map((item) => item['changingThisBreaksApplicationSecurity']).join('\n');
  }

  movePanel(onShow: boolean): void {
    const panelDiv = document.querySelector('#panel > div');

    if (panelDiv && this.span) {
      const optionsDiv = document.getElementsByClassName('options')[0];
      this.optionsCount = optionsDiv ? optionsDiv.childElementCount : 0;

      // prevent the panel from expanding past the bottom of the page after unchecking the checkbox by forcing it to face upwards initially
      if (onShow && this.span.getBoundingClientRect().top > 500 && !panelDiv.className.includes('flipped'))
        panelDiv.className += ' p-overlaypanel-flipped';

      const x = (this.wordLength > 3) ? this.spanX : this.spanX - 15;
      let y: number;
      if (this.checked)
        y = panelDiv.className.includes('flipped') ? this.spanY - 95 : this.spanY + 20;
      else {
        const yOffset = 180 + this.optionsCount * 28; // vertical offset for the upwards panel
        y = panelDiv.className.includes('flipped') ? this.spanY - yOffset : this.spanY + 20;
      }

      const top = y.toString();
      const left = x.toString();
      panelDiv.setAttribute('style', 'top: ' + top + 'px; left: ' + left + 'px; --overlayArrowLeft: 0px;');
    }
  }

  onShow(): void {
    setTimeout(() => {
      this.movePanel(true);
    }, 0);
  }

  check(event: MouseEvent, checked: boolean): void {
    this.checked = checked;
    this.option = '';
    if (this.checked) {
      this.span.classList.add('ignore');
      this.span.classList.remove('untagged');
      this.span.classList.remove('data-id');
      this.span.classList.remove('data-typeid');
    } else {
      this.span.classList.remove('ignore');
      this.span.classList.add('untagged');
    }

    this.panel.toggle(event, this.span);
    // // move the upwards panel to the word's location after (un)checking the checkbox
    // if (this.flipped) {
    //   setTimeout(() => {
    //     this.movePanel(false);
    //   }, 0);
    // }
    this.dirty = true;
    const messageSpan = document.getElementById('save-message');
    messageSpan.innerHTML = 'Измене у току...';
  }

  selectWord(event: MouseEvent, id: number, typeid: number): void {
    this.clickedWord.setAttribute('data-id', id.toString());
    this.clickedWord.setAttribute('data-typeid', typeid.toString());
    this.clickedWord.classList.remove('untagged');
    this.panel.toggle(event, this.span);
    this.dirty = true;
    const messageSpan = document.getElementById('save-message');
    messageSpan.innerHTML = 'Измене у току...';
  }

  updateTaggedText(): void {
    if (this.dirty) {
      const messageSpan = document.getElementById('save-message');
      messageSpan.innerHTML = 'Снимам измене...';
      const container = document.getElementById('para-container');
      const paragraphs = container.getElementsByTagName<'p'>('p');
      const paras = [].slice.call(paragraphs).map((item) => item.innerHTML);
      const text = paras.join('\n');
      this.publikacijaService.updateFragment(this.pubId, this.fragmentNr, text).subscribe(
        (data) => {
          console.log(data);
          this.dirty = false;
          messageSpan.innerHTML = 'Измене су сачуване';
        },
        (error) => {
          console.log(error);
        }
      );
    }
  }

  addLexeme(wordType: number): void {
    let url = '/imenica/add';
    switch (wordType) {
      case 1: url = '/glagol/add'; break;
      case 2: url = '/pridev/add'; break;
    }
    const returnUrl = `/publikacija/${this.pubId}/fragment/${this.fragmentNr}`;
    const word = this.word;
    if (this.option === '')
      this.router.navigate([url], { queryParams: { returnUrl, word } });
  }

  editLexeme(): void {
    // const word = this.option.split(' - ')[0].split(') ')[1]; // (1) тест - именица => тест
    // const type = this.option.split(' - ')[1]; // (1) тест - именица => именица
    // const id = this.options.find(opt => opt.word === word && opt.type === type).id;
    const word = this.word;
    const returnUrl = `/publikacija/${this.pubId}/fragment/${this.fragmentNr}`;
    const url = '/' + this.wordTypesMap[this.selectedWordTypeId] + '/' + this.selectedWordId.toString();
    console.log(url);
    this.router.navigate([url], { queryParams: { returnUrl, word } });
  }

}
