import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { RippleModule } from 'primeng/ripple';
import { DialogModule } from 'primeng/dialog';
import { ShortCollocationComponent } from './short-collocation.component';

@NgModule({
  declarations: [ShortCollocationComponent],
  exports: [
    ShortCollocationComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ButtonModule,
    InputTextModule,
    RippleModule,
    DialogModule,
  ]
})
export class ShortCollocationModule { }
