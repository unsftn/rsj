import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { RippleModule } from 'primeng/ripple';
import { ButtonModule } from 'primeng/button';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { ZamenicaComponent } from './zamenica.component';

const routes: Routes = [{ path: '', component: ZamenicaComponent }]

@NgModule({
  declarations: [ZamenicaComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes),
    InputTextModule,
    RippleModule,
    ButtonModule,
    MyToolbarModule,
  ],
  exports: [RouterModule],
  bootstrap: [ZamenicaComponent]
})
export class ZamenicaModule { }
