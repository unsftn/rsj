import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ReccaService } from '../../../services/reci/';
import { TokenStorageService } from '../../../services/auth/token-storage.service';
import { Recca, toRecca } from '../../../models/reci';

@Component({
  selector: 'app-recca',
  templateUrl: './recca.component.html',
  styleUrls: ['./recca.component.scss']
})
export class ReccaComponent implements OnInit {

  id: number;
  editMode: boolean;
  returnUrl: string;
  sourceWord: string;
  recca: Recca;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private reccaService: ReccaService,
  ) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.returnUrl = params.returnUrl;
      this.sourceWord = params.word;
    });
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          this.recca = { tekst: '', vlasnikID: this.tokenStorageService.getUser().id };
          document.getElementById('tekst').focus();
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe(
            (params) => {
              this.id = +params.id;
              this.reccaService.get(this.id).subscribe({
                next: (item) => {
                  this.recca = toRecca(item);
                },
                error: (error) => {
                  console.log(error);
                  this.messageService.add({
                    severity: 'error',
                    summary: 'Грешка',
                    life: 5000,
                    detail: `Речца није учитана: ${error}`,
                  });
                  this.router.navigate(['/']);
                }
            });
          });
          break;        
      }
    });
  }

  save(): void {
    if (this.editMode) {
      this.reccaService.update({id: this.id, tekst: this.recca.tekst}).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Речца је успешно сачувана.`,
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
    } else {
      this.reccaService.add({tekst: this.recca.tekst}).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Речца је успешно сачувана.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
            this.router.navigate(['/recca', data.id]);
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

  saveAvailable() {
    if (this.tokenStorageService.isEditor())
      return true;
    if (!this.editMode)
      return true;
    if (this.tokenStorageService.getUser().id === this.recca?.vlasnikID)
      return true;
    return false;
  }
}
