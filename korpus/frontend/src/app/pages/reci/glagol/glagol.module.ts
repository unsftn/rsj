import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { RippleModule } from 'primeng/ripple';
import { TabViewModule } from 'primeng/tabview';
import { ButtonModule } from 'primeng/button';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { GlagolComponent } from './glagol.component';

const routes: Routes = [{ path: '', component: GlagolComponent }]

@NgModule({
  declarations: [GlagolComponent],
  imports: [
    CommonModule,
    FormsModule,
    InputTextModule,
    DropdownModule,
    RippleModule,
    TabViewModule,
    ButtonModule,
    MyToolbarModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [GlagolComponent]
})
export class GlagolModule { }
