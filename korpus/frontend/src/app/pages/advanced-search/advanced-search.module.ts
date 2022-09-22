import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { CheckboxModule } from 'primeng/checkbox';
import { SidebarModule } from 'primeng/sidebar';

import { AdvancedSearchComponent } from './advanced-search.component';

const routes: Routes = [{ path: '', component: AdvancedSearchComponent }]

@NgModule({
  declarations: [AdvancedSearchComponent],
  imports: [
    CommonModule,
    FormsModule,
    RippleModule,
    InputTextModule,
    ButtonModule,
    CheckboxModule,
    SidebarModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [AdvancedSearchComponent]
})
export class AdvancedSearchModule { }
