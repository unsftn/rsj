import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Recca } from '../../models/recca';
import { ReccaService } from '../../services/recca/recca.service';

@Component({
  selector: 'recca',
  templateUrl: './recca.component.html',
  styleUrls: ['./recca.component.scss']
})
export class ReccaComponent implements OnInit {

  @Input() recca: Recca;

  @Output() reccaChanged: EventEmitter<Recca> = new EventEmitter();

  id: number;

  constructor(private messageService: MessageService, private reccaService: ReccaService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    if (window.location.href.endsWith('/add'))
      this.recca = {
        tekst: ''
      };
    else {
      this.route.params.subscribe((params) => {
        this.id = +params.id;
      });
      this.getReccaById();
      this.recca = { // test case, delete if getting data from the server
        id: this.id,
        tekst: 'тест',
        version: 1
      };
    }
  }

  changeRecca(): void {
    this.reccaChanged.emit(this.recca);
  }

  async getReccaById() {
    const response: any = await this.reccaService.getRecca(this.id)
      .toPromise()
      .catch(() => {
        this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Тражена речца није пронађена'});
      });
    if (response) {
      this.recca = response.map((item: Recca) => {
        return {
          tekst: item.tekst, id: item.id, version: item.version
        };
      });
    }
  }
}
