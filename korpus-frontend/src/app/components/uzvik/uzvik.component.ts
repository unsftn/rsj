import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Uzvik } from '../../models/uzvik';
import { UzvikService } from '../../services/uzvik/uzvik.service';

@Component({
  selector: 'uzvik',
  templateUrl: './uzvik.component.html',
  styleUrls: ['./uzvik.component.scss']
})
export class UzvikComponent implements OnInit {

  @Input() uzvik: Uzvik;

  @Output() uzvikChanged: EventEmitter<Uzvik> = new EventEmitter();

  id: number;

  constructor(private messageService: MessageService, private uzvikService: UzvikService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    if (window.location.href.endsWith('/add'))
      this.uzvik = {
        tekst: ''
      };
    else {
      this.route.params.subscribe((params) => {
        this.id = +params.id;
      });
      this.getUzvikById();
      this.uzvik = { // test case, delete if getting data from the server
        id: this.id,
        tekst: 'тест'
      };
    }
  }

  changeUzvik(): void {
    this.uzvikChanged.emit(this.uzvik);
  }

  async getUzvikById() {
    const response: any = await this.uzvikService.getUzvik(this.id)
      .toPromise()
      .catch(() => {
        this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Тражени узвик није пронађен'});
      });
    if (response) {
      this.uzvik = response.map((item: Uzvik) => {
        return {
          tekst: item.tekst, id: item.id
        };
      });
    }
  }
}
