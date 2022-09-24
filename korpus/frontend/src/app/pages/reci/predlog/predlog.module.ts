import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { PredlogComponent } from './predlog.component';

const routes: Routes = [{ path: '', component: PredlogComponent }]

@NgModule({
  declarations: [PredlogComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forRoot(routes),
    InputTextModule,
    MyToolbarModule,
  ],
  exports: [RouterModule],
  bootstrap: [PredlogComponent]
})
export class PredlogModule { }
