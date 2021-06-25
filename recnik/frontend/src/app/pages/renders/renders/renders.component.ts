import { Component, OnInit } from '@angular/core';
import { RenderService } from '../../../services/render/';
import { Render } from '../../../models';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-renders',
  templateUrl: './renders.component.html',
  styleUrls: ['./renders.component.scss']
})
export class RendersComponent implements OnInit {
  constructor(private renderService: RenderService, private titleService: Title) {}

  renders: Render[];

  ngOnInit(): void {
    this.titleService.setTitle('Рендери');
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
