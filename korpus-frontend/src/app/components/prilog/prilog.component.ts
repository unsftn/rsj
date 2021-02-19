import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Prilog } from '../../models/prilog';
import { PrilogService } from '../../services/prilog/prilog.service';

@Component({
  selector: 'prilog',
  templateUrl: './prilog.component.html',
  styleUrls: ['./prilog.component.scss']
})
export class PrilogComponent implements OnInit {

  @Input() prilog: Prilog;

  @Output() prilogChanged: EventEmitter<Prilog> = new EventEmitter();

  id: number;

  constructor(private messageService: MessageService, private prilogService: PrilogService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    if (window.location.href.endsWith('/add'))
      this.prilog = {
        tekst: ''
      };
    else {
      this.route.params.subscribe((params) => {
        this.id = +params.id;
      });
      this.getPrilogById();
      this.prilog = { // test case, delete if getting data from the server
        id: this.id,
        tekst: 'тест'
      };
    }
  }

  changePrilog(): void {
    this.prilogChanged.emit(this.prilog);
  }

  async getPrilogById() {
    const response: any = await this.prilogService.getPrilog(this.id)
      .toPromise()
      .catch(() => {
        this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Тражени прилог није пронађен'});
      });
    if (response) {
      this.prilog = response.map((item: Prilog) => {
        return {
          tekst: item.tekst, id: item.id
        };
      });
    }
  }
}
