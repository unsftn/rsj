import {
  Component,
  OnInit,
  OnChanges,
  SimpleChanges,
  Input,
} from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { StaticHtmlService } from '../../services/static-html';

@Component({
  selector: 'app-rendered-odrednice',
  templateUrl: './rendered-odrednice.component.html',
  styleUrls: ['./rendered-odrednice.component.scss'],
})
export class RenderedOdredniceComponent implements OnInit {
  innerHtml: SafeHtml;

  @Input() source: string;
  @Input() isTrusted: boolean;

  constructor(
    private staticHtmlService: StaticHtmlService,
    private domSanitizer: DomSanitizer,
  ) {}

  ngOnInit(): void {
    this.insertStaticView();
  }

  private insertStaticView(): void {
    this.staticHtmlService
      .getStaticHTML(this.source, this.isTrusted)
      .subscribe((response) => {
        this.replaceHtml(response);
      });
  }

  private replaceHtml(innerHTML: string): void {
    this.innerHtml = this.domSanitizer.bypassSecurityTrustHtml(innerHTML);
  }
}
