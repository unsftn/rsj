import { Component, OnInit, Input } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

interface WordType {
  name: string;
}

@Component({
  selector: 'grammarInformations',
  templateUrl: './grammarInformations.component.html',
  styleUrls: ['./grammarInformations.component.scss'],
})
export class GrammarInformationsComponent implements OnInit {
  @Input() isNoun: boolean;
  @Input() isVerb: boolean;
  kinds: string[];

  public selectedKind: string;
  constructor(private primengConfig: PrimeNGConfig) {}

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.kinds = ['Мушки', 'Женски', 'Средњи'];
  }
}
