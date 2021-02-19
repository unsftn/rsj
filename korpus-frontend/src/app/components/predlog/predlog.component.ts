import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Predlog } from '../../models/predlog';
import { PredlogService } from '../../services/predlog/predlog.service';

@Component({
  selector: 'predlog',
  templateUrl: './predlog.component.html',
  styleUrls: ['./predlog.component.scss']
})
export class PredlogComponent implements OnInit {

  @Input() predlog: Predlog;

  @Output() predlogChanged: EventEmitter<Predlog> = new EventEmitter();

  id: number;

  constructor(private messageService: MessageService, private predlogService: PredlogService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    if (window.location.href.endsWith('/add'))
      this.predlog = {
        tekst: ''
      };
    else {
      this.route.params.subscribe((params) => {
        this.id = +params.id;
      });
      this.getPredlogById();
      this.predlog = { // test case, delete if getting data from the server
        id: this.id,
        tekst: 'тест'
      };
    }
  }

  changePredlog(): void {
    this.predlogChanged.emit(this.predlog);
  }

  async getPredlogById() {
    const response: any = await this.predlogService.getPredlog(this.id)
      .toPromise()
      .catch(() => {
        this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Тражени предлог није пронађен'});
      });
    if (response) {
      this.predlog = response.map((item: Predlog) => {
        return {
          tekst: item.tekst, id: item.id
        };
      });
    }
  }
}
