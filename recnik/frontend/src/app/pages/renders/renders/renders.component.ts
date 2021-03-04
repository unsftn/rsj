import { Component, OnInit } from '@angular/core';
import { RenderService } from '../../../services/render/';
import { Render } from '../../../models';

@Component({
  selector: 'app-renders',
  templateUrl: './renders.component.html',
  styleUrls: ['./renders.component.scss']
})
export class RendersComponent implements OnInit {
  constructor(private renderService: RenderService) {}

  renders: Render[];

  ngOnInit(): void {
    this.renderService.getRenderi().subscribe(
      (data) => {
        this.renders = data;
      },
      (err) => {
        console.log(err);
      }
    );
  }

  download(render: Render): void {
    this.renderService.download(render);
  }
}
