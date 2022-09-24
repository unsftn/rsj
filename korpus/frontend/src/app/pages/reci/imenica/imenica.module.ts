import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { RippleModule } from 'primeng/ripple';
import { ButtonModule } from 'primeng/button';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { ImenicaComponent } from './imenica.component';

const routes: Routes = [{ path: '', component: ImenicaComponent }]

@NgModule({
  declarations: [ImenicaComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forRoot(routes),
    InputTextModule,
    DropdownModule,
    RippleModule,
    ButtonModule,
    MyToolbarModule,
  ],
  exports: [RouterModule],
  bootstrap: [ImenicaComponent]
})
export class ImenicaModule { }
