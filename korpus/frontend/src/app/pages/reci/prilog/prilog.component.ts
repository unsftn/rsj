import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Prilog, toPrilog } from '../../../models/reci';
import { PrilogService } from '../../../services/reci';

@Component({
  selector: 'app-prilog',
  templateUrl: './prilog.component.html',
  styleUrls: ['./prilog.component.scss']
})
export class PrilogComponent implements OnInit {

  prilog: Prilog;
  id: number;
  editMode: boolean;
  returnUrl: string;
  sourceWord: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private prilogService: PrilogService,
  ) { }

  ngOnInit(): void {
    this.initNew();
    this.route.queryParams.subscribe((params) => {
      this.returnUrl = params.returnUrl;
      this.sourceWord = params.word;
    });
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          document.getElementById('komparativ').focus();
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe(
            (params) => {
              this.id = +params.id;
              this.prilogService.get(this.id).subscribe({
                next: (item) => {
                  this.prilog = toPrilog(item);
                },
                error: (error) => {
                  console.log(error);
                  this.messageService.add({
                    severity: 'error',
                    summary: 'Грешка',
                    life: 5000,
                    detail: 'Број није учитан',
                  });
                  this.router.navigate(['/']);
                }
              });
            });
          break;
      }
    });
  }

  initNew(): void {
    this.prilog = this.prilogService.new();
  }

  check(): boolean {
    try {
      this.assert(this.prilog.komparativ.trim().length === 0, 'Мора се унети компаратив.');
      return true;
    } catch (e) {
      return false;
    }
  }

  assert(condition: boolean, message: string): void {
    if (condition) {
      this.messageService.add({
        severity: 'error',
        summary: 'Грешка',
        life: 0,
        detail: message,
      });
      throw new Error();
    }
  }

  save(): void {
    if (!this.check()) return;
    console.log('Snimanje priloga:', this.prilog);
    if (!this.editMode) {
      this.prilogService.add(this.prilog).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Прилог је успешно сачуван.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
            this.router.navigate(['/prilog', data.id]);
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
      this.prilogService.update(this.prilog).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Прилог је успешно сачуван.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
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