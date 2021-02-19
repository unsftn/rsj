import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Veznik } from '../../models/veznik';
import { VeznikService } from '../../services/veznik/veznik.service';

@Component({
  selector: 'veznik',
  templateUrl: './veznik.component.html',
  styleUrls: ['./veznik.component.scss']
})
export class VeznikComponent implements OnInit {

  @Input() veznik: Veznik;

  @Output() veznikChanged: EventEmitter<Veznik> = new EventEmitter();

  id: number;

  constructor(private messageService: MessageService, private veznikService: VeznikService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    if (window.location.href.endsWith('/add'))
      this.veznik = {
        tekst: ''
      };
    else {
      this.route.params.subscribe((params) => {
        this.id = +params.id;
      });
      this.getVeznikById();
      this.veznik = { // test case, delete if getting data from the server
        id: this.id,
        tekst: 'тест'
      };
    }
  }

  changeVeznik(): void {
    this.veznikChanged.emit(this.veznik);
  }

  async getVeznikById() {
    const response: any = await this.veznikService.getVeznik(this.id)
      .toPromise()
      .catch(() => {
        this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Тражени везник није пронађен'});
      });
    if (response) {
      this.veznik = response.map((item: Veznik) => {
        return {
          tekst: item.tekst, id: item.id
        };
      });
    }
  }
}
