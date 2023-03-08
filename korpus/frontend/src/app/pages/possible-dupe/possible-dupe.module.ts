import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { DialogModule } from 'primeng/dialog';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { PossibleDupeComponent } from './possible-dupe.component';

@NgModule({
  declarations: [
    PossibleDupeComponent
  ],
  imports: [
    CommonModule,
    DialogModule,
    TableModule,
    ButtonModule,
    RippleModule,
    RouterModule,
  ],
  exports: [PossibleDupeComponent]
})
export class PossibleDupeModule { }
