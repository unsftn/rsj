import { Component, OnInit } from '@angular/core';
import { Injectable } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
@Injectable({ providedIn: 'root' })
export class HomeComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}

  ngOnInit() {
    this.primengConfig.ripple = true;
  }
}
