import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { HttpClient } from '@angular/common/http';

interface Qualificator {
  name: string;
  abbreviation: string;
  id: number;
}

@Component({
  selector: 'qualificator',
  templateUrl: './qualificator.component.html',
  styleUrls: ['./qualificator.component.scss'],
})
export class QualificatorComponent implements OnInit {
  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {}

  qualificators: Qualificator[];

  @Input() selectedQualificators: Qualificator[];

  @Output()
  selectedQualificatorsChanged: EventEmitter<
    Qualificator[]
  > = new EventEmitter();

  selectQualificator() {
    this.selectedQualificatorsChanged.emit(this.selectedQualificators);
  }

  async fetchQualificatiors() {
    const response: any = await this.httpClient
      .get('api/odrednice/kvalifikator/')
      .toPromise();

    if (response) {
      this.qualificators = response.map((item) => {
        return { name: item.naziv, abbreviation: item.skracenica, id: item.id };
      });
    }
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.fetchQualificatiors();
  }
}
