import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { PridevService } from 'src/app/services/reci/pridev.service';
import { Pridev, toPridev } from '../../../models/reci';

@Component({
  selector: 'app-pridev',
  templateUrl: './pridev.component.html',
  styleUrls: ['./pridev.component.scss']
})
export class PridevComponent implements OnInit {

  pridev: Pridev;

  id: number;
  editMode: boolean;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private pridevService: PridevService,
  ) { }

  ngOnInit(): void {
    this.initNew();
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          setTimeout(() => { document.getElementById('mnomjed1').focus(); });
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe(
            (params) => {
              this.id = +params.id;
              this.pridevService.get(this.id).subscribe({
                  next: (item) => {
                  this.pridev = toPridev(item);
                  console.log(this.pridev);
                },
                error: (error) => {
                  console.log(error);
                  this.messageService.add({
                    severity: 'error',
                    summary: 'Грешка',
                    life: 5000,
                    detail: 'Придев није учитан',
                  });
                  this.router.navigate(['/']);
              }});
            });
          break;
      }
    });
  }

  initNew(): void {
    this.pridev = this.pridevService.new();
  }

  check(): boolean {
    return true;
  }

  save(): void {
    if (!this.check()) return;
    if (!this.editMode) {
      this.pridevService.add(this.pridev).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Придев је успешно сачуван.`,
          });
          this.router.navigate(['/pridev', data.id]);
        },
        error: (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: `Неуспешно снимање: ${error}`,
          });
        }
      });
    } else {
      this.pridevService.update(this.pridev).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Придев је успешно сачуван.`,
          });
        },
        error: (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: `Неуспешно снимање: ${error}`,
          });
        }
      });
    }
  }
}
