import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { PaginatorModule } from 'primeng/paginator';
import { DropdownModule } from 'primeng/dropdown';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { SearchComponent } from './search.component';

const routes: Routes = [{ path: '', component: SearchComponent }];

@NgModule({
  declarations: [SearchComponent],
  imports: [
    CommonModule,
    PaginatorModule,
    DropdownModule,
    ProgressSpinnerModule,
    OverlayPanelModule,
    ButtonModule,
    RippleModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [SearchComponent]
})
export class SearchModule { }
