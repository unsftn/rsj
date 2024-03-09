import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { DialogModule } from 'primeng/dialog';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { AreYouSureComponent } from './are-you-sure.component';


@NgModule({
  declarations: [
    AreYouSureComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    DialogModule,
    ButtonModule,
    RippleModule
  ],
  exports: [AreYouSureComponent]
})
export class AreYouSureModule { }
