import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { PredlogComponent } from './predlog.component';
import { PossibleDupeModule } from '../../possible-dupe/possible-dupe.module';

const routes: Routes = [{ path: '', component: PredlogComponent }]

@NgModule({
  declarations: [PredlogComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes),
    InputTextModule,
    MyToolbarModule,
    PossibleDupeModule,
  ],
  exports: [RouterModule],
  bootstrap: [PredlogComponent]
})
export class PredlogModule { }
