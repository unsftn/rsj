import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { ToolbarModule } from 'primeng/toolbar';
import { DialogModule } from 'primeng/dialog';
import { TableModule } from 'primeng/table';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { PubListComponent } from './pub-list.component';

const routes: Routes = [{ path: '', component: PubListComponent }]

@NgModule({
  declarations: [PubListComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    ToolbarModule,
    DialogModule,
    TableModule,
    InputTextModule,
    ButtonModule,
    RippleModule,
  ],
  exports: [RouterModule],
  bootstrap: [PubListComponent]
})
export class PubListModule { }
