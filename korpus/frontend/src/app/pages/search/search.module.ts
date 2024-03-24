import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { PaginatorModule } from 'primeng/paginator';
import { DropdownModule } from 'primeng/dropdown';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { TooltipModule } from 'primeng/tooltip';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { SearchComponent } from './search.component';
import { NvlPipe } from '../../utils/nvl.pipe';

const routes: Routes = [{ path: '', component: SearchComponent }];

@NgModule({
  declarations: [SearchComponent, NvlPipe],
  imports: [
    CommonModule,
    PaginatorModule,
    DropdownModule,
    ProgressSpinnerModule,
    OverlayPanelModule,
    ButtonModule,
    RippleModule,
    TooltipModule,
    DialogModule,
    InputTextModule,
    AutoCompleteModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [SearchComponent],
})
export class SearchModule { }
